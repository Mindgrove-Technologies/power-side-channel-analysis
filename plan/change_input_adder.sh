a_line=43
b_line=44
vcd_line=44

a=32
b=16
vcd=2

cd ..
cd ..
home=$(pwd)

add=$home/c-classperformancetest/directed-tests/add.S
script=$home/c-classperformancetest/Scripts/run_dir_test.sh


echo "Changing a & b values in add.S"
sed -i "$a_line s/.*/.dword $a/" $add
sed -i "$b_line s/.*/.dword $b/" $add
echo "Changing VCD File number"
sed -i -E "$vcd_line s/[0-9]+.vcd/$vcd.vcd/" $script