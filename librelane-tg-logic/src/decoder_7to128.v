// 7-bit to 128-bit one-hot decoder
module decoder_7to128 (
    input  wire [6:0]   dec_in,
    output wire [127:0] dec_out
);

    assign dec_out = 128'b1 << dec_in;

endmodule
