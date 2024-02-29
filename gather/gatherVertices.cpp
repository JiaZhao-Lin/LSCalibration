#include <iostream>
#include <string>

#include <TChain.h>
#include <TDirectory.h>
#include <TF1.h>
#include <TFile.h>
#include <TH1.h>
#include <TParameter.h>
#include <TTree.h>

struct gatheredVertices {
    TH1F* hist;
    TF1* func;
    gatheredVertices(TH1F* h, TF1* fu) : hist(h), func(fu) {}
    double avg() { return hist->GetMean(); }
    double avgerr() { return hist->GetMeanError(); }
    double fit() { return func->GetParameter(1); }
    double fiterr() { return func->GetParError(1); }
    void Write(std::string name) {
        ((TH1F*)hist->Clone((name+"_hist").c_str()))->Write();
        func->Write((name+"_func").c_str());
    }
    void Delete() {
        hist->Delete();
        func->Delete();
    }
};

const gatheredVertices gatherVertices(TTree* tree, std::string obs, std::string cond) {
    // get mean value of observable
    tree->Draw((obs+"*1.0e4>>hfirst").c_str(), cond.c_str(), "goff");
    TH1F* hfirst = (TH1F*)gDirectory->Get("hfirst");
    const double mean = hfirst->GetMean();
    hfirst->Delete();

    // get arithmetic average of observable
    TH1F* hsecond = new TH1F("hsecond", "", 1000, mean-500.0, mean+500.0);
    tree->Draw((obs+"*1.0e4>>hsecond").c_str(), cond.c_str(), "goff");

    // fit observable with Gaussian function
    TF1* fitfunction = new TF1("fitfunction", "gaus(0)", mean-500.0, mean+500.0);
    hsecond->Fit(fitfunction, "NQ");

    // return results
    return gatheredVertices(hsecond, fitfunction);
}

void gatherVerticesScan(
    const std::string inputfiles,
    const std::string outputname,
    const std::string name,
    const std::string obs,
    const int nSteps,
    const std::pair<int, int>* timestamps,
    const int runnumber,
    const int* lumisections,
    const std::string cond
) {
    // prepare input data
    TChain* inputs = new TChain("vertices");
    inputs->Add(inputfiles.c_str());

    // create output file
    TFile* output = TFile::Open(outputname.c_str(), "RECREATE");

    // loop over all steps
    for(int iStep=0; iStep<nSteps; iStep++) {
        std::cout << "Now at Scan " << name << ", Step " << iStep << std::endl;
        const std::string prefix = "step"+std::to_string(iStep)+"_";

        // timestamp selection
        gatheredVertices resTS = gatherVertices(
            inputs, obs, cond+"&&timestamp>"+std::to_string(timestamps[iStep].first)
                             +"&&timestamp<"+std::to_string(timestamps[iStep].second)
        );
        resTS.Write(prefix+"ts");
        resTS.Delete();

        // lumisection selection
        gatheredVertices resLS = gatherVertices(
            inputs, obs, cond+"&&run=="+std::to_string(runnumber)
                             +"&&lumisection=="+std::to_string(lumisections[iStep])
        );
        resLS.Write(prefix+"ls");
        resLS.Delete();
    }

    // close output file
    output->Close();
}

void gatherVerticesScan(
    const std::string inputfiles,
    const std::string outputname,
    const std::string name,
    const std::string obs,
    const int nSteps,
    const std::pair<int, int>* timestamps,
    const int runnumber,
    const std::string cond
) {
    // prepare input data
    TChain* inputs = new TChain("vertices");
    inputs->Add(inputfiles.c_str());

    // create output file
    TFile* output = TFile::Open(outputname.c_str(), "RECREATE");

    // loop over all steps
    for(int iStep=0; iStep<nSteps; iStep++) {
        std::cout << "Now at Scan " << name << ", Step " << iStep << std::endl;
        const std::string prefix = "step"+std::to_string(iStep)+"_";

        // timestamp selection
        gatheredVertices resTS = gatherVertices(
            inputs, obs, cond+"&&timestamp>"+std::to_string(timestamps[iStep].first)
                             +"&&timestamp<"+std::to_string(timestamps[iStep].second)
        );
        resTS.Write(prefix+"ts");
        resTS.Delete();
    }

    // close output file
    output->Close();
}

void gatherVerticesHeadon(
    const std::string inputfiles,
    const std::string outputname,
    const std::string name,
    const std::string obs,
    const std::pair<int, int>* timestamps,
    const std::string cond
) {
    // prepare input data
    TChain* inputs = new TChain("vertices");
    inputs->Add(inputfiles.c_str());

    // create output file
    TFile* output = TFile::Open(outputname.c_str(), "RECREATE");

    // loop over all steps
    for(int iStep=0; iStep<2; iStep++) {
        std::cout << "Now at Scan " << name << ", head-on " << (iStep==0 ? "before" : "after") << " the scan" << std::endl;
        const std::string prefix = "headon"+std::to_string(iStep)+"_";

        // timestamp selection
        gatheredVertices resTS = gatherVertices(
            inputs, obs, cond+"&&timestamp>"+std::to_string(timestamps[iStep].first)
                             +"&&timestamp<"+std::to_string(timestamps[iStep].second)
        );
        resTS.Write(prefix+"ts");
        resTS.Delete();
    }

    // close output file
    output->Close();
}
