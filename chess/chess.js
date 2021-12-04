var white_piece;
var black_piece;
var white_pos = [4, 7];
var black_pos = [4, 0];
var speed = 500; 
var length = 1000;
var width = length;
var height = length;
var piecel = length/8;
var turn = false;

var id;

function play() {
	white_piece = document.getElementById("white");
	black_piece = document.getElementById("black");
	white_piece.style.top = white_pos[1] * piecel + "px";
	white_piece.style.left = white_pos[0] * piecel + "px";
	black_piece.style.top = black_pos[1] * piecel + "px";
	black_piece.style.left = black_pos[0] * piecel + "px";

	id = setInterval(frame, speed);
}

function coord_to_string(coord) {
	var alpha = ["A", "B", "C", "D", "E", "F", "G", "H"];
	return "K" + alpha[coord[0]] + (8 - coord[1]);
}

function frame() {
	if (turn) {
		var moves = [];
		if (black_pos[0] < 7) moves.push([1, 0]);
		if (black_pos[0] > 0) moves.push([-1, 0]);
		if (black_pos[1] < 7) moves.push([0, 1]);
		if (black_pos[1] > 0) moves.push([0, -1]);

		if (black_pos[0] < 7 && black_pos[1] < 7) moves.push([1, 1]);
		if (black_pos[0] > 0 && black_pos[1] > 0) moves.push([-1, -1]);
		if (black_pos[0] < 7 && black_pos[1] > 0) moves.push([1, -1]);
		if (black_pos[0] > 0 && black_pos[1] < 7) moves.push([-1, 1]);

		for (i = 0; i < moves.length; i++) {
			test = [black_pos[0] + moves[i][0], black_pos[1] + moves[i][1]];
			for (a = -1; a <= 1; a++) {
				for (b = -1; b <= 1; b++) {
					if (test[0] + a == white_pos[0] && test[1] + b == white_pos[1]) {
						moves.splice(i, 1);
						console.log("white king too close can't play move to " + coord_to_string(test));
						i--;
						a = 2;
						b = 2;
					}
				}
			}
		}

		var move = moves[Math.floor(Math.random() * Math.floor(moves.length))];

		black_pos[0] += move[0];
		black_pos[1] += move[1];

		console.log("Black plays " + coord_to_string(black_pos));
		turn = false;
	} else {
		var moves = [];
		if (white_pos[0] < 7) moves.push([1, 0]);
		if (white_pos[0] > 0) moves.push([-1, 0]);
		if (white_pos[1] < 7) moves.push([0, 1]);
		if (white_pos[1] > 0) moves.push([0, -1]);

		if (white_pos[0] < 7 && white_pos[1] < 7) moves.push([1, 1]);
		if (white_pos[0] > 0 && white_pos[1] > 0) moves.push([-1, -1]);
		if (white_pos[0] < 7 && white_pos[1] > 0) moves.push([1, -1]);
		if (white_pos[0] > 0 && white_pos[1] < 7) moves.push([-1, 1]);

		for (i = 0; i < moves.length; i++) {
			test = [white_pos[0] + moves[i][0], white_pos[1] + moves[i][1]];
			for (a = -1; a <= 1; a++) {
				for (b = -1; b <= 1; b++) {
					if (test[0] + a == black_pos[0] && test[1] + b == black_pos[1]) {
						moves.splice(i, 1);
						console.log("black king too close can't play move to " + coord_to_string(test));
						i--;
						a = 2;
						b = 2;
					}
				}
			}
		}
		var move = moves[Math.floor(Math.random() * Math.floor(moves.length))];
		white_pos[0] += move[0];
		white_pos[1] += move[1];
		console.log("White plays " + coord_to_string(white_pos) + "\n");
		turn = true;

	}
	white_piece.style.top = white_pos[1] * piecel + "px";
	white_piece.style.left = white_pos[0] * piecel + "px";
	black_piece.style.top = black_pos[1] * piecel + "px";
	black_piece.style.left = black_pos[0] * piecel + "px";
}
