// Testbench for decoder_7to128
// 実行方法:
//   iverilog -o tb_decoder_7to128 tb_decoder_7to128.v decoder_7to128.v
//   vvp tb_decoder_7to128
`timescale 1ns / 1ps

module tb_decoder_7to128;

    reg  [6:0]   in;
    wire [127:0] out;

    reg  [127:0] expected;
    integer      i;
    integer      errors;

    decoder_7to128 dut (
        .dec_in  (in),
        .dec_out (out)
    );

    initial begin
        $dumpfile("tb_decoder_7to128.vcd");
        $dumpvars(0, tb_decoder_7to128);

        errors = 0;

        for (i = 0; i < 128; i = i + 1) begin
            in = i;
            #10;
            expected = 128'b0;
            expected[i] = 1'b1;
            if (out !== expected) begin
                $display("NG: in=%b (%0d) out=%h expected=%h", in, i, out, expected);
                errors = errors + 1;
            end
        end

        if (errors == 0)
            $display("PASS: all 128 patterns OK");
        else
            $display("FAIL: %0d errors", errors);

        $finish;
    end

endmodule
