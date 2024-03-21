import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

def generate_first_chart(students, courses):
    plt.pie(students, labels=courses)
    plt.title('Students per program')

    plt.savefig("site/static/first.png")


def generate_second_chart(percents, courses):
    plt.subplots(figsize=(18, 18))
    plt.bar(courses, percents, width=0.7)
    plt.title('Overall attendance')

    plt.savefig("site/static/second.png")
