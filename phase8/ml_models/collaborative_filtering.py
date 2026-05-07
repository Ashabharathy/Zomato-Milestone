"""
Neural Collaborative Filtering Implementation

Advanced matrix factorization using deep neural networks
for restaurant recommendations based on user-item interactions.
"""

import torch
import torch.nn as nn
import numpy as np
import pandas as pd
from typing import List, Tuple, Dict, Optional
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset, DataLoader
import torch.optim as optim


class RestaurantDataset(Dataset):
    """Dataset for user-restaurant interactions"""
    
    def __init__(self, interactions: pd.DataFrame):
        self.users = interactions['user_id'].values
        self.restaurants = interactions['restaurant_id'].values
        self.ratings = interactions['rating'].values
    
    def __len__(self):
        return len(self.users)
    
    def __getitem__(self, idx):
        return (
            torch.tensor(self.users[idx], dtype=torch.long),
            torch.tensor(self.restaurants[idx], dtype=torch.long),
            torch.tensor(self.ratings[idx], dtype=torch.float)
        )


class NeuralCollaborativeFiltering(nn.Module):
    """Neural Collaborative Filtering model for restaurant recommendations"""
    
    def __init__(
        self, 
        num_users: int, 
        num_restaurants: int, 
        embedding_dim: int = 64,
        hidden_layers: List[int] = [128, 64, 32],
        dropout_rate: float = 0.2
    ):
        super(NeuralCollaborativeFiltering, self).__init__()
        
        self.num_users = num_users
        self.num_restaurants = num_restaurants
        self.embedding_dim = embedding_dim
        
        # Embedding layers
        self.user_embedding = nn.Embedding(num_users, embedding_dim)
        self.restaurant_embedding = nn.Embedding(num_restaurants, embedding_dim)
        
        # MLP layers for interaction
        layers = []
        input_dim = embedding_dim * 2
        
        for hidden_dim in hidden_layers:
            layers.extend([
                nn.Linear(input_dim, hidden_dim),
                nn.ReLU(),
                nn.Dropout(dropout_rate),
                nn.BatchNorm1d(hidden_dim)
            ])
            input_dim = hidden_dim
        
        layers.append(nn.Linear(input_dim, 1))
        self.mlp = nn.Sequential(*layers)
        
        # Initialize weights
        self._init_weights()
    
    def _init_weights(self):
        """Initialize model weights"""
        nn.init.xavier_uniform_(self.user_embedding.weight)
        nn.init.xavier_uniform_(self.restaurant_embedding.weight)
        
        for layer in self.mlp:
            if isinstance(layer, nn.Linear):
                nn.init.xavier_uniform_(layer.weight)
                nn.init.constant_(layer.bias, 0)
    
    def forward(self, user_ids: torch.Tensor, restaurant_ids: torch.Tensor) -> torch.Tensor:
        """Forward pass"""
        user_emb = self.user_embedding(user_ids)  # [batch_size, embedding_dim]
        restaurant_emb = self.restaurant_embedding(restaurant_ids)  # [batch_size, embedding_dim]
        
        # Concatenate embeddings
        concat_emb = torch.cat([user_emb, restaurant_emb], dim=1)  # [batch_size, 2*embedding_dim]
        
        # Pass through MLP
        output = self.mlp(concat_emb)  # [batch_size, 1]
        
        return output.squeeze(-1)  # [batch_size]
    
    def predict(self, user_id: int, restaurant_ids: List[int]) -> np.ndarray:
        """Predict ratings for a user and multiple restaurants"""
        self.eval()
        with torch.no_grad():
            user_tensor = torch.tensor([user_id] * len(restaurant_ids), dtype=torch.long)
            restaurant_tensor = torch.tensor(restaurant_ids, dtype=torch.long)
            
            predictions = self.forward(user_tensor, restaurant_tensor)
            return predictions.numpy()
    
    def recommend_top_k(
        self, 
        user_id: int, 
        candidate_restaurants: List[int], 
        k: int = 10,
        exclude_seen: Optional[List[int]] = None
    ) -> List[Tuple[int, float]]:
        """Get top-k recommendations for a user"""
        if exclude_seen is None:
            exclude_seen = []
        
        # Filter out already seen restaurants
        candidates = [r for r in candidate_restaurants if r not in exclude_seen]
        
        if not candidates:
            return []
        
        # Get predictions
        predictions = self.predict(user_id, candidates)
        
        # Create list of (restaurant_id, prediction) tuples
        recommendations = list(zip(candidates, predictions))
        
        # Sort by prediction and return top-k
        recommendations.sort(key=lambda x: x[1], reverse=True)
        
        return recommendations[:k]


class CollaborativeFilteringTrainer:
    """Trainer for Neural Collaborative Filtering model"""
    
    def __init__(
        self, 
        model: NeuralCollaborativeFiltering,
        learning_rate: float = 0.001,
        weight_decay: float = 1e-6,
        device: str = 'cpu'
    ):
        self.model = model
        self.device = device
        self.model.to(device)
        
        self.optimizer = optim.Adam(
            model.parameters(), 
            lr=learning_rate, 
            weight_decay=weight_decay
        )
        self.criterion = nn.MSELoss()
        
        self.train_losses = []
        self.val_losses = []
    
    def train_epoch(self, dataloader: DataLoader) -> float:
        """Train for one epoch"""
        self.model.train()
        total_loss = 0.0
        num_batches = 0
        
        for user_ids, restaurant_ids, ratings in dataloader:
            user_ids = user_ids.to(self.device)
            restaurant_ids = restaurant_ids.to(self.device)
            ratings = ratings.to(self.device)
            
            self.optimizer.zero_grad()
            
            predictions = self.model(user_ids, restaurant_ids)
            loss = self.criterion(predictions, ratings)
            
            loss.backward()
            self.optimizer.step()
            
            total_loss += loss.item()
            num_batches += 1
        
        return total_loss / num_batches
    
    def validate(self, dataloader: DataLoader) -> float:
        """Validate the model"""
        self.model.eval()
        total_loss = 0.0
        num_batches = 0
        
        with torch.no_grad():
            for user_ids, restaurant_ids, ratings in dataloader:
                user_ids = user_ids.to(self.device)
                restaurant_ids = restaurant_ids.to(self.device)
                ratings = ratings.to(self.device)
                
                predictions = self.model(user_ids, restaurant_ids)
                loss = self.criterion(predictions, ratings)
                
                total_loss += loss.item()
                num_batches += 1
        
        return total_loss / num_batches
    
    def train(
        self, 
        train_loader: DataLoader, 
        val_loader: DataLoader, 
        epochs: int = 100,
        patience: int = 10,
        verbose: bool = True
    ) -> Dict[str, List[float]]:
        """Train the model"""
        best_val_loss = float('inf')
        patience_counter = 0
        
        for epoch in range(epochs):
            train_loss = self.train_epoch(train_loader)
            val_loss = self.validate(val_loader)
            
            self.train_losses.append(train_loss)
            self.val_losses.append(val_loss)
            
            if verbose and epoch % 10 == 0:
                print(f"Epoch {epoch}: Train Loss = {train_loss:.4f}, Val Loss = {val_loss:.4f}")
            
            # Early stopping
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                patience_counter = 0
                # Save best model
                torch.save(self.model.state_dict(), 'best_ncf_model.pth')
            else:
                patience_counter += 1
                if patience_counter >= patience:
                    if verbose:
                        print(f"Early stopping at epoch {epoch}")
                    break
        
        # Load best model
        self.model.load_state_dict(torch.load('best_ncf_model.pth'))
        
        return {
            'train_losses': self.train_losses,
            'val_losses': self.val_losses
        }


def create_sample_data(num_users: int = 1000, num_restaurants: int = 500, num_interactions: int = 10000) -> pd.DataFrame:
    """Create sample interaction data for testing"""
    np.random.seed(42)
    
    # Generate random interactions
    user_ids = np.random.randint(0, num_users, num_interactions)
    restaurant_ids = np.random.randint(0, num_restaurants, num_interactions)
    
    # Generate ratings (1-5 scale)
    ratings = np.random.randint(1, 6, num_interactions)
    
    # Create DataFrame
    interactions = pd.DataFrame({
        'user_id': user_ids,
        'restaurant_id': restaurant_ids,
        'rating': ratings
    })
    
    # Remove duplicates
    interactions = interactions.drop_duplicates(subset=['user_id', 'restaurant_id'])
    
    return interactions


def main():
    """Example usage of Neural Collaborative Filtering"""
    print("🤖 Neural Collaborative Filtering for Restaurant Recommendations")
    
    # Create sample data
    interactions = create_sample_data()
    print(f"📊 Created {len(interactions)} user-restaurant interactions")
    
    # Get unique counts
    num_users = interactions['user_id'].nunique()
    num_restaurants = interactions['restaurant_id'].nunique()
    
    print(f"👥 Users: {num_users}, 🍽️ Restaurants: {num_restaurants}")
    
    # Split data
    train_data, val_data = train_test_split(interactions, test_size=0.2, random_state=42)
    
    # Create datasets and dataloaders
    train_dataset = RestaurantDataset(train_data)
    val_dataset = RestaurantDataset(val_data)
    
    train_loader = DataLoader(train_dataset, batch_size=256, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=256, shuffle=False)
    
    # Create model
    model = NeuralCollaborativeFiltering(
        num_users=num_users,
        num_restaurants=num_restaurants,
        embedding_dim=64,
        hidden_layers=[128, 64, 32]
    )
    
    # Create trainer
    trainer = CollaborativeFilteringTrainer(model, learning_rate=0.001)
    
    # Train model
    print("🚀 Training Neural Collaborative Filtering model...")
    history = trainer.train(train_loader, val_loader, epochs=50, verbose=True)
    
    # Test recommendations
    test_user = 0
    candidate_restaurants = list(range(50))  # First 50 restaurants
    
    recommendations = model.recommend_top_k(test_user, candidate_restaurants, k=5)
    
    print(f"\n🎯 Top 5 recommendations for User {test_user}:")
    for i, (restaurant_id, score) in enumerate(recommendations, 1):
        print(f"{i}. Restaurant {restaurant_id}: {score:.4f}")
    
    print("✅ Neural Collaborative Filtering implementation complete!")


if __name__ == "__main__":
    main()
