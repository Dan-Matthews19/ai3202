Dan Matthews AI3202 Assignment 3.

To run: python AStar.py <World> <Hueristic>

Options for World: Select W1 for World1.txt and W2 for World2.txt.

Options for Hueristic: Select: H1 for Manhattan Distance hueristic and H2 for Pythagorean Hueristic.

Examples:
python AStar.py W1 H2
python AStar.py W1 H1
python AStar.py W2 H2
python AStar.py W2 H1

Second Hueristic explained:

I decided to use a pythagorean distance hueristic for my second hueristic, because I felt it could anticipate a more accurate estimate of distance that just the manhattan distance itself. I felt with the way the graph was being searched, AStar would have a more acurate estimate if thinking about the hypotunuse distance to the goal from any point on the matrix rather that the total x,y distance.