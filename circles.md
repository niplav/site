[home](./index.md)
-------------------

*author: niplav, created: 2019-06-21, modified: 2019-12-02, language: english, status: notes, importance: 4, confidence: highly likely*

> __It is currently unknown how many ways exist to [arrange
> n circles](https://www.youtube.com/watch?v=bRIL9kMJJSc) in
> the affine plane. However, for up to 5 circles, the [number is
> known](https://oeis.org/A250001). This page attempts to classify the
> current known combinations.__

Circle Combinations
===================

Characteristic Description of a Circle Combination
--------------------------------------------------

Any unintersected plane is contained by n circles. How many planes exist
that are contained in n circles?

The characteristic description of a circle combination lists
the number of planes contained by n circles, in ascending order.
For example, the following circle has the description 1,2,1,1:

![Circle Combination 3_6](img/circle_combinations/3_6.png)

There is only one plane not contained by any circles (the outer plane),
2 planes only contained by one circle, 1 plane contained by 2 circles,
and 1 plane (the innermost circle) contained by all 3 circles.

As one can see, the outer plane is counted as well.

Conjecture: The characteristic description of a circle is a unique
identifier of the circle combination described (no 2 circle combinations
have the same characteristic description).

1 Circle
--------

<table>
<tbody>
	<tr>
		<td>Image</td>
		<td>Unintersected lines</td>
		<td>Line intersections</td>
		<td>Unintersected planes</td>
		<td>Characteristic description</td>
	</tr>
	<tr>
		<td><img src="./img/circle_combinations/1_1.png"></img></td>
		<td>1</td>
		<td>0</td>
		<td>1</td>
		<td>1,1</td>
	</tr>
</tbody>
</table>

2 Circles
----------

<table>
<tbody>
	<tr>
		<td>Image</td>
		<td>Unintersected lines</td>
		<td>Line intersections</td>
		<td>Unintersected planes</td>
		<td>Characteristic description</td>
	</tr>
	<tr>
		<td><img src="./img/circle_combinations/2_1.png"></img></td>
		<td>2</td>
		<td>0</td>
		<td>3</td>
		<td>1,2,0</td>
	</tr>
	<tr>
		<td><img src="./img/circle_combinations/2_2.png"></img></td>
		<td>4</td>
		<td>2</td>
		<td>4</td>
		<td>1,2,1</td>
	</tr>
	<tr>
		<td><img src="./img/circle_combinations/2_3.png"></img></td>
		<td>2</td>
		<td>0</td>
		<td>3</td>
		<td>1,1,1</td>
	</tr>
</tbody>
</table>

3 Circles
---------

<table>
<tbody>
	<tr>
		<td>Image</td>
		<td>Unintersected lines</td>
		<td>Line intersections</td>
		<td>Unintersected planes</td>
		<td>Characteristic description</td>
	</tr>
	<tr>
		<td><img src="./img/circle_combinations/3_1.png"></img></td>
		<td>3</td>
		<td>0</td>
		<td>4</td>
		<td>1,3,0,0</td>
	</tr>
	<tr>
		<td><img src="./img/circle_combinations/3_2.png"></img></td>
		<td>5</td>
		<td>2</td>
		<td>5</td>
		<td>1,3,1,0</td>
	</tr>
	<tr>
		<td><img src="./img/circle_combinations/3_3.png"></img></td>
		<td>8</td>
		<td>4</td>
		<td>6</td>
		<td>1,3,3,0</td>
	</tr>
	<tr>
		<td><img src="./img/circle_combinations/3_4.png"></img></td>
		<td>5</td>
		<td>2</td>
		<td>5</td>
		<td>1,2,2,0</td>
	</tr>
	<tr>
		<td><img src="./img/circle_combinations/3_5.png"></img></td>
		<td>8</td>
		<td>4</td>
		<td>6</td>
		<td>1,2,2,1</td>
	</tr>
	<tr>
		<td><img src="./img/circle_combinations/3_6.png"></img></td>
		<td>5</td>
		<td>2</td>
		<td>5</td>
		<td>1,2,1,1</td>
	</tr>
	<tr>
		<td><img src="./img/circle_combinations/3_7.png"></img></td>
		<td>12</td>
		<td>6</td>
		<td>8</td>
		<td>1,3,3,1</td>
	</tr>
	<tr>
		<td><img src="./img/circle_combinations/3_8.png"></img></td>
		<td>3</td>
		<td>0</td>
		<td>4</td>
		<td>1,2,1,0</td>
	</tr>
	<tr>
		<td><img src="./img/circle_combinations/3_9.png"></img></td>
		<td>3</td>
		<td>0</td>
		<td>4</td>
		<td>1,1,2,0</td>
	</tr>
	<tr>
		<td><img src="./img/circle_combinations/3_10.png"></img></td>
		<td>5</td>
		<td>2</td>
		<td>4</td>
		<td>1,1,2,1</td>
	<tr>
		<td><img src="./img/circle_combinations/3_11.png"></img></td>
		<td>3</td>
		<td>0</td>
		<td>4</td>
		<td>1,1,1,1</td>
	</tr>
	<tr>
		<td><img src="./img/circle_combinations/3_12.png"></img></td>
		<td>12</td>
		<td>6</td>
		<td>8</td>
		<td>1,4,2,1</td>
	</tr>
	<tr>
		<td><img src="./img/circle_combinations/3_13.png"></img></td>
		<td>12</td>
		<td>6</td>
		<td>8</td>
		<td>1,2,4,1</td>
	</tr>
	<tr>
		<td><img src="./img/circle_combinations/3_14.png"></img></td>
		<td>12</td>
		<td>6</td>
		<td>8</td>
		<td>2,3,3,0</td>
	</tr>
</tbody>
</table>
