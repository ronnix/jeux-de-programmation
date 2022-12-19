<?php

function part1(string $text): int {
	return max(elfCalories($text));
}

function elfCalories(string $text): array {
	$paragraphs = explode("\n\n", $text);
	return array_map("calories", $paragraphs);
}

function calories(string $paragraph): int {
	$lines = explode("\n", $paragraph);
	return array_sum(array_map("intval", $lines));
}

function readInput(string $filename): string {
	$f = fopen($filename, "r");
	$contents = fread($f, filesize($filename));
	fclose($f);
	return $contents;
}

$PUZZLE_INPUT = readInput("day-01.txt");

print_r(part1($PUZZLE_INPUT));
print_r(PHP_EOL);

function part1Compact(string $text): int {
	return max(
		array_map(
			function ($paragraph) {
				$lines = explode("\n", $paragraph);
				return array_sum(array_map("intval", $lines));
			},
			explode("\n\n", $text)
		)
	);
}

print_r(part1Compact($PUZZLE_INPUT));
print_r(PHP_EOL);

