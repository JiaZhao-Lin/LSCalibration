#include "prepare.cpp"


void prepare_HIPhysicsRawPrime()
{
	// std::string inFileName = "PixVertex_HIPhysicsRawPrime0_PromptReco.root";
	// std::string inFileName = "PixVertex_HIPhysicsRawPrime1_PromptReco.root";
	std::string inFileName = "PixVertex_HIPhysicsRawPrime10_PromptReco.root";

	std::string inFileDir = "inFiles/" + inFileName;
	std::string outFileDir = "outFiles/prepared_" + inFileName;

	Prepare prep;
	
	prep.init(outFileDir); // choose an output file name
	prep.add(inFileDir); // repeat for every input file
	prep.close();

}
