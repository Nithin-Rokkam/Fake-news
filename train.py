from app.models import FakeNewsModel
import os

def main():
    model = FakeNewsModel()
    true_path = os.path.join('data', 'true.csv')
    fake_path = os.path.join('data', 'fake.csv')
    model.train(true_path, fake_path)

if __name__ == '__main__':
    main()