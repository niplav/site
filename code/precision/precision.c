#include <math.h>
#include <time.h>
#include <stddef.h>
#include <stdlib.h>
#include <stdio.h>

#define LEN1 4

struct prediction {
	int outcome;
	double forecast;
};

struct prediction example1[]={
	{1, 0.8},
	{0, 0.4},
	{0, 0.65},
	{1, 0.99}
};

struct prediction example2[]={
	{1, 0.8},
	{0, 0.4},
	{0, 0.65},
	{1, 0.9}
};

struct prediction example3[]={
	{0, 0.8},
	{1, 0.4},
	{1, 0.65},
	{0, 0.9}
};

double logit(double p) {
	return log(p/(1-p));
}

double logistic(double p) {
	return 1/(1+exp(-p));
}

double mse(struct prediction forecasts[], size_t nforecasts) {
	double se=0;
	for(size_t i=0; i<nforecasts; i++) {
		se+=pow(forecasts[i].outcome-forecasts[i].forecast, 2);
	}
	return se/nforecasts;
}

double perturbed_score_difference(struct prediction forecasts[], size_t nforecasts, double perturbation, int samples) {
	double se=0;
	double noise, perturbed;
	for(size_t i=0; i<samples; i++) {
		for(size_t j=0; j<nforecasts; j++) {
			perturbed=logit(forecasts[j].forecast);
			noise=perturbation*(1.0*(rand()-RAND_MAX/2))/(RAND_MAX);
			perturbed=logistic(noise+perturbed);
			se+=pow(forecasts[j].outcome-perturbed, 2);
		}
	}
	double perturbed_mse=se/(samples*nforecasts);
	return perturbed_mse-mse(forecasts, nforecasts);
}

int main(int argc, char** argv) {
	double scorediff;
	srand(time(NULL));

	for(double sigma=0; sigma<=0.5; sigma+=0.001) {
		scorediff=perturbed_score_difference(example3, LEN1, sigma, 10000);
		printf("%f,%.9f\n", sigma, scorediff);
	}

	return 0;
}
