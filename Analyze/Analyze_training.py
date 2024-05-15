import matplotlib.pyplot as plt

class TrainingPlotter:
  def plot_loss(self, trainer):
        plt.figure(figsize=(12, 4))

        plt.plot(range(trainer.n_epochs), trainer.epoch_training_losses, label='Training Loss')
        plt.plot(range(trainer.n_epochs), trainer.epoch_testing_losses, label='Testing Loss')

        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.title('Training and Testing Loss over Epochs')
        plt.legend()
        plt.show()  
        
        #TODO
