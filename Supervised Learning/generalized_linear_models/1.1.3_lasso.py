from sklearn import linear_model

classifier = linear_model.Lasso(alpha=0.1)
print(classifier.fit([[0, 0], [1, 1]], [0, 1]))
print(classifier.predict([1, 1]))