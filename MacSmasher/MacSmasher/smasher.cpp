#pragma once

#include <sstream>
#include <iostream>
#include <fstream>
#include "smasher.h"

#define CL_FILE "smashMD5.cl"

void smasher::set_platform() {
	cl_uint ret_num_platforms;
	ret = clGetPlatformIDs(1, &platform, &ret_num_platforms);

	// log data
	stringstream s;
	s << "Set platform to ID " << platform << ". NUMBER_OF_PLATFORMS = " << ret_num_platforms << ". Return code = " << getErrorString(ret);
	_log(s.str());
}

void smasher::set_device() {
	cl_uint ret_num_devices;
	ret = clGetDeviceIDs(platform, CL_DEVICE_TYPE_GPU, 1, &device, &ret_num_devices);

	// log data
	stringstream s;
	s << "Set device to ID " << device << ". NUMBER_OF_DEVICES = " << ret_num_devices << ". Return code = " << getErrorString(ret);
	_log(s.str());
}

void smasher::create_context() {
	context = clCreateContext(NULL, 1, &device, NULL, NULL, &ret);

	// log creation
	stringstream s;
	s << "Created context. Return code = " << getErrorString(ret);
	_log(s.str());
}

void smasher::create_command_queue() {
	command_queue = clCreateCommandQueue(context, device, NULL, &ret);

	// log creation
	stringstream s;
	s << "Created command queue. Return code = " << getErrorString(ret);
	_log(s.str());
}

void smasher::read_cl() {
	// open file
	fstream file(CL_FILE);

	// get file size
	int size = file.tellg();
	file.seekg(ios::beg);

	// read CL code
	stringstream buffer;
	buffer << file.rdbuf();
	file.close();

	code = buffer.str();

	// log compilation
	stringstream s;
	s << "Read and compiled CL-code. Return code = " << getErrorString(ret);
	_log(s.str());
}

void smasher::create_program() {
	// turn string into char buffer
	int count = code.size();
	char *buffer = &code[0];

	// compile code
	program = clCreateProgramWithSource(context, 1, (const char**)&buffer, (const size_t *)&count, &ret);
	ret = clBuildProgram(program, 1, &device, NULL, NULL, NULL);

	// log creation
	stringstream s;
	s << "Created program. Return code = " << getErrorString(ret);
	_log(s.str());
}

void smasher::create_kernel() {
	kernel = clCreateKernel(program, FUNC_NAME, &ret);

	// log creation
	stringstream s;
	s << "Created kernel. Return code = " << getErrorString(ret);
	_log(s.str());
}

void smasher::init() {
	_log("Beginning initialization...");

	set_platform();
	set_device();
	create_context();
	create_command_queue();
	read_cl();
	create_program();
	create_kernel();

	_log("Finished initialization");
}

/*Operation specific functions*/

/*TODO*/
void smasher::create_memory(const int block_num, char* out) {
	stringstream s;

	input = clCreateBuffer(context, 
		CL_MEM_READ_WRITE | CL_MEM_COPY_HOST_PTR, 
		block_num * BLOCK_SIZE, 
		input_data.data(), 
		&ret);
	s << "Created input memory. count = " << BLOCK_SIZE * BLOCK_SIZE << ". Return code = " << getErrorString(ret);

	output = clCreateBuffer(context, 
		CL_MEM_READ_WRITE | CL_MEM_COPY_HOST_PTR, 
		block_num * BLOCK_SIZE, 
		out,
		&ret);
	s << endl << "Created output memory. count = " << BLOCK_SIZE * BLOCK_SIZE << ". Return code = " << getErrorString(ret);

	_log(s.str());
}

/*TODO*/
void smasher::get_results(vector<TYPE> &out) {
	const size_t count = out.size();

	// read result into out
	ret = clEnqueueReadBuffer(command_queue, output, CL_TRUE, 0, count * sizeof(TYPE), out.data(), 0, NULL, NULL);

	// log reading
	stringstream s;
	s << "Read from output GPU memory. Return code = " << getErrorString(ret);
	_log(s.str());
}

/*TODO*/
void smasher::set_args(const cl_uint count) {
	stringstream s;

	ret = clSetKernelArg(kernel, 0, sizeof(cl_mem), &input);
	s << "Set argument1 to input memory. Return code = " << getErrorString(ret);

	ret = clSetKernelArg(kernel, 1, sizeof(cl_mem), &output);
	s << endl << "Set argument2 to output memory. Return code = " << getErrorString(ret);

	ret = clSetKernelArg(kernel, 2, sizeof(cl_uint), &count);
	s << endl << "Set argument3 to count. Return code = " << getErrorString(ret);

	_log(s.str());
}

void smasher::run(const size_t count) {
	stringstream s1, s2;

	// run sorting
	ret = clEnqueueNDRangeKernel(command_queue, kernel, 1, 0, &count, NULL, NULL, NULL, NULL);
	clFinish(command_queue);
}

/*TODO*/
char* smasher::sort(const int block_num) {
	char* out;

	create_memory(block_num, out);
	set_args(count);
	run(count);

	get_results(out);
	return out;
}

smasher::smasher() {
	init();
}
smasher::~smasher() {
	ret = clFlush(command_queue);
	ret = clFinish(command_queue);
	ret = clReleaseKernel(kernel);
	ret = clReleaseProgram(program);
	ret = clReleaseMemObject(input);
	ret = clReleaseMemObject(output);
	ret = clReleaseCommandQueue(command_queue);
	ret = clReleaseContext(context);
}