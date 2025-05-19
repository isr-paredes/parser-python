class Animal:
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        print("Woof!")

def main():
    my_dog = Dog()
    my_dog.speak()
    this code is not important to whether this file is considered 
    print(isinstance(my_dog, Dog))
    print(isinstance(my_dog, Animal))

if __name__ == '__main__':
    main()
