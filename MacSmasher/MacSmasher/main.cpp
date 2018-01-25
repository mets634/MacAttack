#include <iostream>
#include <fstream>
#include <string>
#include "smasher.h"
#include "log.h"

using namespace std;


bool smash_block(const uint block_num);

static smasher s;
static char cmpto[MD5_SIZE];

int main(int argc, char* argv[]) {
	if (argc < 3) // no block # supplied
		return -5;
	if (!s.get_ready()) {
		_log("Critical -- Failed to initiate smasher");
		return SMASHER_INIT_ERROR;
	}

	_log("Getting cmpto value...");
	memcpy(cmpto, argv[1], MD5_SIZE); // copy input value to cmpto

	smash_block(atoi(argv[2])); // smash

	_log("\nDone...");
	return EXIT_SUCCESS;
}

bool smash_block(const uint block_num) {
	// run smasher on block
	_log("Running smasher...");
	int res = s.smash(block_num, cmpto);

#ifdef LOG
	if (res == -1)
		_log("Hash not found =(");
	else
		_log("Hash found! =)");
#endif

	cout << res; // output result
	return true;
}