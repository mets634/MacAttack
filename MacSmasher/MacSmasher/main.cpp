#include <iostream>
#include <fstream>
#include <string>
#include "smasher.h"
#include "log.h"

using namespace std;

bool smash_block();

static smasher s;
static char cmpto[MD5_SIZE];

int main() {
	if (!s.get_ready()) {
		_log("Critical -- Failed to initiate smasher");
		return SMASHER_INIT_ERROR;
	}

	_log("Awaiting cmpto value...");
	cin.read(cmpto, MD5_SIZE); // read cmpto hash

	while (smash_block()); // keep smashing blocks

	_log("\nDone...");
	return EXIT_SUCCESS;
}

bool smash_block() {
	// read block number
	int block_num;
	cin >> block_num;

	// negative input means exit
	if (block_num < 0)
		return false;

	// run smasher on block
	_log("Running smasher...");
	int res = s.smash(block_num, cmpto);

	// parse results

#ifdef LOG
	if (res == -1)
		_log("Hash not found =(");
	else
		_log("Hash found! =)");
#endif

	cout << res; // output result
	return true;
}