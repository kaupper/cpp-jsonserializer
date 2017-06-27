#include <iostream>
#include <cassert>
#include <cmath>

#include "ExampleStructures.h"
#include "Example2Structures.h"
#include "StructConverter.h"

using namespace ex;
using namespace ex2;
using namespace jsonserializer;


bool isNear(double d1, double d2)
{
    return std::fabs(d1 - d2) < 0.0001;
}

int main()
{
    json j {
        {"string_field_trans", "string test"},
        {"int_field_trans", 12345},
        {"bool_field_trans", false},
        {"int_field", 54321},
        {"bool_field", true}
    };
    ExampleStruct3 ex3 = Converter::FromJSON<ExampleStruct3>(
        {
            {"test", 1.234}
        }
    );
    ExampleStruct2 ex2 = Converter::FromJSON<ExampleStruct2>(j);
    ExampleStruct1 *ex1 = ex2.GetStructField();

    assert(ex1->GetStringFieldTransValue() == "string test");
    assert(ex1->GetIntFieldTransValue() == 12345);
    assert(ex1->GetBoolFieldTransValue() == false);
    assert(ex2.GetBoolFieldValue() == true);
    assert(ex2.GetIntFieldValue() == 54321);
    assert(isNear(ex3.GetTestValue(), 1.234));

    assert(j == Converter::ToJSON(ex2));

    try {
        // should throw due to the lack of an required field
        Converter::FromJSON<ExampleStruct3>({});
        assert(false);
    } catch (const ConverterException &ex) {
        
    }
    
    try {
        // should not throw because all other fields are optional
        Converter::FromJSON<ExampleStruct1>({{"int_field_trans", 12345}});
    } catch (const ConverterException &ex) {
        assert(false);
    }
    return 0;
}