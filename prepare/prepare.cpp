#include <string>

#include <TFile.h>
#include <TTree.h>

const int maxArraySize = 50;

class Prepare {
public:
    void init(std::string);
    void add(std::string);
    void close();

protected:
    // user-defined information
    virtual bool condition() { return true; }
    virtual void addtofile() {}

    // input file structure
    struct {
        unsigned int timeStamp_begin;
        int run, LS, bunchCrossing, nVtx;
        int vtx_nTrk[maxArraySize];
        float vtx_x[maxArraySize], vtx_y[maxArraySize], vtx_xError[maxArraySize], vtx_yError[maxArraySize];
        bool vtx_isValid[maxArraySize], vtx_isFake[maxArraySize], vtx_isGood[maxArraySize];
    } Input;

    // output file structure
    struct {
        // for vertex position
        int vtx_nTrk;
        float vtx_x, vtx_y, vtx_xError, vtx_yError;
        // for number of vertices
        int nVtx[50];
    } Output;
    TFile* outputfile = nullptr;
    TTree* positionstree = nullptr;
    TTree* nverticestree = nullptr;

};

void Prepare::init(std::string filename) {
    // open output file
    outputfile = TFile::Open(filename.c_str(), "RECREATE");

    // create tree with vertex positions
    positionstree = new TTree("vertices", "Selected vertices for length scale calibration");
    positionstree->Branch("timestamp", &Input.timeStamp_begin, "timestamp/i");
    positionstree->Branch("run", &Input.run, "run/I");
    positionstree->Branch("lumisection", &Input.LS, "lumisection/I");
    positionstree->Branch("bunchcrossing", &Input.bunchCrossing, "bunchcrossing/I");
    positionstree->Branch("nTrk", &Output.vtx_nTrk, "nTrk/I");
    positionstree->Branch("x", &Output.vtx_x, "x/F");
    positionstree->Branch("y", &Output.vtx_y, "y/F");
    positionstree->Branch("xError", &Output.vtx_xError, "xError/F");
    positionstree->Branch("yError", &Output.vtx_yError, "yError/F");

    // create tree with vertex counts
    nverticestree = new TTree("counts", "Number of vertices for length scale calibration");
    nverticestree->Branch("timestamp", &Input.timeStamp_begin, "timestamp/i");
    nverticestree->Branch("run", &Input.run, "run/I");
    nverticestree->Branch("lumisection", &Input.LS, "lumisection/I");
    nverticestree->Branch("bunchcrossing", &Input.bunchCrossing, "bunchcrossing/I");
    nverticestree->Branch("nVtx", Output.nVtx, "nVtx[50]/I");
}

void Prepare::add(std::string filename) {
    // read input file
    TFile* inputfile = TFile::Open(filename.c_str());
    TTree* inputtree = (TTree*)inputfile->Get("lumi/tree");
    inputtree->SetBranchAddress("timeStamp_begin", &Input.timeStamp_begin);
    inputtree->SetBranchAddress("bunchCrossing", &Input.bunchCrossing);
    inputtree->SetBranchAddress("run", &Input.run);
    inputtree->SetBranchAddress("LS", &Input.LS);
    inputtree->SetBranchAddress("nVtx", &Input.nVtx);
    inputtree->SetBranchAddress("vtx_nTrk", &Input.vtx_nTrk);
    inputtree->SetBranchAddress("vtx_x", &Input.vtx_x);
    inputtree->SetBranchAddress("vtx_y", &Input.vtx_y);
    inputtree->SetBranchAddress("vtx_xError", &Input.vtx_xError);
    inputtree->SetBranchAddress("vtx_yError", &Input.vtx_yError);
    inputtree->SetBranchAddress("vtx_isValid", &Input.vtx_isValid);
    inputtree->SetBranchAddress("vtx_isFake", &Input.vtx_isFake);
    inputtree->SetBranchAddress("vtx_isGood", &Input.vtx_isGood);

    // loop over all events
    const long long int nentries = inputtree->GetEntries();
    for(long long int ientry=0; ientry<nentries; ientry++) {
        inputtree->GetEntry(ientry);

        // check central condition
        if(!condition()) continue;

        // reset number of vertices
        for(int i=0; i<50; i++) Output.nVtx[i] = 0;

        // loop over all vertices
        for(int iInput=0; iInput<Input.nVtx; iInput++) {
            if(    iInput>=maxArraySize
                || !Input.vtx_isValid[iInput]
                || Input.vtx_isFake[iInput]
                || !Input.vtx_isGood[iInput]
            ) continue;

            // evaluate number of vertices
            const int nTrk = Input.vtx_nTrk[iInput]>50 ? 50 : Input.vtx_nTrk[iInput];
            for(int iTrk=0; iTrk<nTrk; iTrk++) Output.nVtx[iTrk]++;

            // fill tree with positions
            Output.vtx_nTrk = Input.vtx_nTrk[iInput];
            Output.vtx_x = Input.vtx_x[iInput];
            Output.vtx_y = Input.vtx_y[iInput];
            Output.vtx_xError = Input.vtx_xError[iInput];
            Output.vtx_yError = Input.vtx_yError[iInput];
            positionstree->Fill();
        }

        // fill tree with counts
        nverticestree->Fill();
    }

    // close input file
    inputfile->Close();
}

void Prepare::close() {
    // write results to output file
    outputfile->cd();
    positionstree->Write();
    nverticestree->Write();
    addtofile();

    // close file
    outputfile->Close();
}
