#include <stdio.h>

#include <stdlib.h>
#include <string.h>

#include "socklib.h"
#include "AI.h"

extern char	**Argv;
extern int	Argc;

int main(int argc, char *argv[])
{
    xpilot_setargv(argc, argv);
    return !xpilot_launch();
}
