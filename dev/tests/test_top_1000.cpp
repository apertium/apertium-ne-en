#include<iostream>
#include<vector>
#include<cmath>
#include<cstdlib>
#include<cstdio>
#include<fstream>
#include<string>
using namespace std;
int limited_rand(int limit)
{
  int r, d = RAND_MAX / limit;
  limit *= d;
  do { r = rand(); } while (r >= limit);
  return r / d;
}
int main()
{ 
  vector<string> vs;
  vector<int> v;
  string line;
  string myinput;
  string brk="\n";
  string com="\"";
  string ltp=" | lt-proc ne-en.automorf.bin";
  ifstream myfile ("hitparade_stripped.txt");
  if (myfile.is_open())
  {
    while (myfile.good())
    {
      getline (myfile,line);
      string mycm=com+line+com;
      //cout<<line<<endl;
      myinput= "echo "+mycm+ltp+brk;
      //system(myinput);
      //Changes made here
     // cout<<myinput;
     vs.push_back(myinput);
    }
    myfile.close();
  }
  else 
    cout<<"Unable to open the file"<<endl;
  
  for(int i=0;i<=999;i++)
  {
    //To take random
    //v.push_back(limited_rand(330272));
    //To take only top 1000
    v.push_back(i);
  }
  //for(int i=0;i<=999;i++)
    //cout<<vs[v[i]];
    for(int j=0;j<=999;j++)
    {
      string t;
      t=vs[v[j]];
      const char* c= t.c_str();
      system(c);
    }
  return 0;
}