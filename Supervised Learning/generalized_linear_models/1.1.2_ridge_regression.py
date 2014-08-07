from sklearn import linear_model

classifier = linear_model.Ridge(alpha=0.5)
print(classifier.fit([[0, 0], [0, 0], [1, 1]], [0, .1, 1]))
print(classifier.coef_)
print(classifier.intercept_)

print('Starting RidgeCV')
print('=' * 80)
classifier = linear_model.RidgeCV(alphas=[0.1, 1.0, 10.0])
print(classifier.fit([[0, 0], [0, 0], [1, 1]], [0, .1, 1]))
print(classifier.alpha_)
print(classifier.coef_)
