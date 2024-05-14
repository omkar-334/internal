from model import Model

if __name__ == "__main__":
    model = Model()

    text = input("enter prompt - ")
    response = model.generate(text)
    print(response)
