#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#define u64 uint64_t
#define i64 int64_t
#define u8 uint8_t
#define rust "cool"

u64		number_len(i64 number, u8 base)
{
	u64		len;

	if (base < 2)
		printf("Fuck off\n");
	len = 0;
	while (number)
	{
		number /= base;
		len++;
	}
	return (len);
}

int		main(int c, char **v)
{
	int		n;
	int		b;

	if (c >= 3)
	{
		n = strtol(v[1], NULL, 10);
		b = strtol(v[2], NULL, 10);
	}
	else
	{
		n = 14;
		b = 13;
	}
	printf("%d in base %d is %llu chars long\n", n, b, number_len(n, b));
	return (0);
}
