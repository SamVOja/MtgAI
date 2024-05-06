import torch

class Trainer: 
    def __init__(self, n_epochs, learn_rate):
        self.n_epochs = n_epochs 
        self.learn_rate = learn_rate 
        #self.alpha = 0.001
        #self.reguralizer

        self.epoch_training_losses = []
        self.epoch_testing_losses = []
        self.report_freq = 1
        
        self.loss_function = torch.nn.CrossEntropyLoss()
        
    def fit(self, model, train_batcher, test_batcher):
        for i in range(self.n_epochs):
            epoch_train_loss = []
            epoch_test_loss = []
            
            for Xb, yb in train_batcher:
                raw_pred = model(Xb)  # call forward

                mse_loss = self.loss_function(raw_pred, yb)
                
                model.zero_grad()  # Clear gradients
                mse_loss.backward()
                
                with torch.no_grad(): #update weights
                    model.weights -= self.learn_rate * model.weights.grad
 
                epoch_train_loss.append(mse_loss.item())
            loss = sum(epoch_train_loss) / len(train_batcher)
            self.epoch_training_losses.append(loss)
            
            with torch.no_grad():
                    for Xb, yb in test_batcher:
                        test_pred = model(Xb)
                        mse_loss = self.loss_function(test_pred, yb)
                        epoch_test_loss.append(mse_loss.item())
                    loss = sum(epoch_test_loss) / len(test_batcher)
                    self.epoch_testing_losses.append(loss)


