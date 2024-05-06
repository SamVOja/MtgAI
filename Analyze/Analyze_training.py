import matplotlib.pyplot as plt

class TrainingPlotter:
    def plot_loss(self, trainer):
        plt.figure(figsize=(12, 4))

        plt.plot(range(trainer.n_epochs), trainer.epoch_training_losses)
        plt.plot(range(trainer.n_epochs), trainer.epoch_testing_losses)

        plt.show()
        
        #TODO
