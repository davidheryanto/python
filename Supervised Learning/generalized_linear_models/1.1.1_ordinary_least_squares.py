from sklearn import linear_model

classifier = linear_model.LinearRegression()
print(classifier.fit([[0, 0], [1, 1], [2, 2]], [0, 1, 2]))
print(classifier.coef_)