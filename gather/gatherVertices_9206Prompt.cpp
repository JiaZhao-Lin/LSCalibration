#include <string>

#include "gatherVertices.cpp"
#include "gatherVertices_9206.cpp"


const std::string inFileName = "prepared_PixVertex_HIPhysicsRawPrime10_PromptReco";
const std::string inFileDir = "../prepare/outFiles/" + inFileName + ".root";

const std::string xobs = "x";
const std::string yobs = "y";
const std::string cond = "nTrk>=5";

//remove prepared_ from inFileName
const std::string outFileDir = "outFiles/gathered_9206Prompt_" + inFileName.substr(9);

void gatherVertices_9206Prompt(int iScan=-1) {

	cout << "Gathering vertices from " << inFileDir << endl;
	cout << "Output directory: " << outFileDir << endl;

	if(iScan>1) {
		std::cout << "Specify a number between 0 and 1" << std::endl;
		return;
	}
	if(iScan<0 || iScan==0) gatherVerticesScan(inFileDir, outFileDir+"X1.root", "X1", xobs, nStepsX1, timestampsX1, runnumberX1, cond);
	if(iScan<0 || iScan==1) gatherVerticesScan(inFileDir, outFileDir+"Y1.root", "Y1", yobs, nStepsY1, timestampsY1, runnumberY1, cond);
}
