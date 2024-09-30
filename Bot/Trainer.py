import torch

class Trainer: 
    def __init__(self, n_epochs, learn_rate):
        self.n_epochs = n_epochs 
        self.learn_rate = learn_rate 

        self.epoch_training_losses = []
        self.epoch_testing_losses = []
        
        self.loss_function = torch.nn.CrossEntropyLoss()
        
    def fit(self, model, train_batcher, test_batcher):
        optimizer = optim.SGD(model.parameters(), lr=self.learn_rate, weight_decay=1e-4)
        for i in range(self.n_epochs):
            epoch_train_loss = []
            epoch_test_loss = []
            
            for Xb, yb in train_batcher:
                raw_pred = model(Xb)  # call forward

                loss = self.loss_function(raw_pred, yb)
                
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                
                with torch.no_grad(): #weight values between 0 and 1
                    model.weights.data.clamp_(min=0, max=1)
                    
                epoch_train_loss.append(loss.item())
            loss_sum = sum(epoch_train_loss) / len(train_batcher)
            self.epoch_training_losses.append(loss_sum)
            
            with torch.no_grad():
                    for Xb, yb in test_batcher:
                        test_pred = model(Xb)
                        loss = self.loss_function(test_pred, yb)
                        epoch_test_loss.append(loss.item())
                    loss_sum = sum(epoch_test_loss) / len(test_batcher)
                    self.epoch_testing_losses.append(loss_sum)





