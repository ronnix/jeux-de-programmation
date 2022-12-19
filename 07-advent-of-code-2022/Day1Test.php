<?php

use PHPUnit\Framework\TestCase;

include "day-01.php";

const EXAMPLE_INPUT = "1000
2000
3000

4000

5000
6000

7000
8000
9000

10000";

class Day1Test extends TestCase {

	public function testExampleInput(): void {
		$this->assertEquals(24000, part1(EXAMPLE_INPUT));
	}
}

