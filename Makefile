all:
	g++ -I src/include -L src/lib -o main 3DEngine.cpp -lmingw32 -lSDL2main -lSDL2