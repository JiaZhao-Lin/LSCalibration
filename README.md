# Length Scale Calibration

This is a collection of scripts used to perform the length scale calibration with vertex data of the CMS experiment. Codes are adapted from Joscha Knolle.

## 1) prepare

The first step is to extract the required information from the centrally stored data files and fill them into custom ROOT trees.
Typically, this step has to be performed on `lxplus`.
Interactively with `root`, do:

	.L prepare/prepare.cpp
	Prepare prep;
	prep.init("outputfile.root"); // choose an output file name
	prep.add("inputfile.root"); // repeat for every input file
	prep.close();

To add a preselection based on timestamps or lumisections, define a subclass of `Prepare` which overrides the `bool Prepare::condition()` method.

## 2) gather

The second step is to collect the per-step information from the vertex data needed for the length scale analysis.
This step can be performed locally if the output files from the preparation step have been downloaded.
To extract the average vertex position of a step, do interactively with `root`:

	.L gather/gatherVertices.cpp
	TChain* input = new TChain("vertices");
	input->Add("inputfile.root"); // repeat for every input file
	result = gatherVertices(input, "x", "nTrk>=14 && timestamp>=1440468844 && timestamp<=1440468880"); // adjust selection as necessary
	std::cout << "average: " << result.avg() << " +- " << result.avgerr() << std::endl;
	std::cout << "fitted mean: " << result.fit() << " +- " << result.fiterr() << std::endl;

To plot the vertex distribution of each step, use the script from the `plot` directory:

	sh plot/plotVerticesPerStep.sh file.root 10 output_ "The title"
		# 1st argument: output file from gatherVertices.cpp
		# 2nd argument: number of scan steps
		# 3rd argument: directory and/or prefix for output files
		# 4th argument: title for the legend of the plots

To store the mean values of each step into a text file, use the script:

    python gather/gatherVerticesSummary.py inputfile.root 10 5 > outputfile.txt
        # 2nd argument: total number of steps
        # 3rd argument: number of steps per scan direction

## 3) positions

The third step is to prepare the nominal beamspot positions for each scan step, as well as to derive corrections on these based on beam position monitor (BPM) measurements.
The BPM data has to be accessible from the OrbitDriftsCorr repository.
To prepare the BPM data, do interactively with `python`: