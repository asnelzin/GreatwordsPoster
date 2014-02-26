import twitter
import config
import greatwords


def main():
    choices = []
    numbers = [str(i) for i in range(11)][1:]
    while True:
        for i in range(10):
            statuses = greatwords.get_statuses()
            choices.append(statuses)
            print(str(i + 1) + ': ' + str(statuses))
        choice = input()
        if choice in numbers:
            break
        choices = []

    for status in choices[int(choice) - 1]:
        print(status)
        twitter.post_update(config.secret_keys, status)

if __name__ == '__main__':
    main()








