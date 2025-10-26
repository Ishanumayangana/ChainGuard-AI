import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import json


class AIModule:
    """AI/ML Module for blockchain analytics and security"""
    
    def __init__(self):
        self.anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
        self.transaction_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
    
    def extract_features(self, block_data):
        """Extract features from blockchain data"""
        features = []
        
        if isinstance(block_data, list):
            for block in block_data:
                feature_vector = [
                    block.get('index', 0),
                    block.get('nonce', 0),
                    len(str(block.get('data', ''))),
                    len(block.get('hash', '')),
                    len(block.get('previous_hash', ''))
                ]
                features.append(feature_vector)
        else:
            feature_vector = [
                block_data.get('index', 0),
                block_data.get('nonce', 0),
                len(str(block_data.get('data', ''))),
                len(block_data.get('hash', '')),
                len(block_data.get('previous_hash', ''))
            ]
            features.append(feature_vector)
        
        return np.array(features)
    
    def train_anomaly_detector(self, blockchain_data):
        """Train anomaly detection model"""
        try:
            features = self.extract_features(blockchain_data)
            
            if len(features) < 2:
                # Generate synthetic training data
                synthetic_features = self._generate_synthetic_data(100)
                features = np.vstack([features, synthetic_features])
            
            features_scaled = self.scaler.fit_transform(features)
            self.anomaly_detector.fit(features_scaled)
            self.is_trained = True
            
            return {"status": "success", "samples_trained": len(features)}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def detect_anomaly(self, block_data):
        """Detect anomalies in blockchain blocks"""
        try:
            if not self.is_trained:
                return {"is_anomaly": False, "score": 0, "message": "Model not trained"}
            
            features = self.extract_features(block_data)
            features_scaled = self.scaler.transform(features)
            
            prediction = self.anomaly_detector.predict(features_scaled)
            score = self.anomaly_detector.score_samples(features_scaled)
            
            is_anomaly = prediction[0] == -1
            
            return {
                "is_anomaly": bool(is_anomaly),
                "anomaly_score": float(score[0]),
                "confidence": float(abs(score[0])),
                "status": "anomaly_detected" if is_anomaly else "normal"
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _generate_synthetic_data(self, n_samples):
        """Generate synthetic blockchain data for training"""
        np.random.seed(42)
        synthetic = []
        
        for i in range(n_samples):
            feature_vector = [
                i,  # index
                np.random.randint(1000, 100000),  # nonce
                np.random.randint(50, 500),  # data length
                64,  # hash length (SHA-256)
                64 if i > 0 else 1  # previous hash length
            ]
            synthetic.append(feature_vector)
        
        return np.array(synthetic)
    
    def predict_transaction_risk(self, transaction_data):
        """Predict risk level of a transaction"""
        try:
            # Extract transaction features
            amount = transaction_data.get('amount', 0)
            timestamp = transaction_data.get('timestamp', 0)
            data_size = len(str(transaction_data.get('data', '')))
            
            # Simple rule-based risk assessment
            risk_score = 0
            
            if amount > 10000:
                risk_score += 30
            elif amount > 5000:
                risk_score += 15
            
            if data_size > 1000:
                risk_score += 20
            
            # Determine risk level
            if risk_score > 40:
                risk_level = "HIGH"
            elif risk_score > 20:
                risk_level = "MEDIUM"
            else:
                risk_level = "LOW"
            
            return {
                "risk_score": risk_score,
                "risk_level": risk_level,
                "factors": {
                    "amount": amount,
                    "data_size": data_size
                }
            }
        except Exception as e:
            return {"error": str(e)}
    
    def analyze_blockchain_patterns(self, blockchain_data):
        """Analyze patterns in blockchain"""
        try:
            if not blockchain_data or len(blockchain_data) < 2:
                return {"message": "Insufficient data for analysis"}
            
            # Calculate statistics
            nonces = [block.get('nonce', 0) for block in blockchain_data]
            timestamps = [block.get('timestamp', 0) for block in blockchain_data]
            
            # Calculate time differences between blocks
            time_diffs = []
            for i in range(1, len(timestamps)):
                time_diffs.append(timestamps[i] - timestamps[i-1])
            
            analysis = {
                "total_blocks": len(blockchain_data),
                "average_nonce": float(np.mean(nonces)) if nonces else 0,
                "max_nonce": int(np.max(nonces)) if nonces else 0,
                "min_nonce": int(np.min(nonces)) if nonces else 0,
                "avg_block_time": float(np.mean(time_diffs)) if time_diffs else 0,
                "mining_difficulty_trend": "increasing" if len(nonces) > 1 and nonces[-1] > nonces[0] else "stable"
            }
            
            return analysis
        except Exception as e:
            return {"error": str(e)}
    
    def get_blockchain_health_score(self, blockchain_data, is_valid):
        """Calculate overall blockchain health score"""
        try:
            health_score = 100
            
            # Deduct points for invalid chain
            if not is_valid:
                health_score -= 50
            
            # Check block consistency
            if len(blockchain_data) > 1:
                for i in range(1, len(blockchain_data)):
                    current = blockchain_data[i]
                    previous = blockchain_data[i-1]
                    
                    if current.get('previous_hash') != previous.get('hash'):
                        health_score -= 10
            
            # Ensure score is between 0 and 100
            health_score = max(0, min(100, health_score))
            
            status = "excellent" if health_score >= 90 else \
                     "good" if health_score >= 70 else \
                     "fair" if health_score >= 50 else "poor"
            
            return {
                "health_score": health_score,
                "status": status,
                "is_valid": is_valid
            }
        except Exception as e:
            return {"error": str(e)}
