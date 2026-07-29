    package ising_pkg;

        // ISING
        localparam int PBIT_NUM_MAX = 128;
        localparam int PBIT_NUM = 100;

        localparam int TERM_WEIGHT_W = 8;
        localparam int TERM_WEIGHT_FRAC = 7;

        localparam int SUM_W = 16;
        localparam int SUM_FRAC = 7;

        localparam int BETA_W = 16;
        localparam int BETA_FRAC = 11;

        localparam int PROBABILITY_W = 12;
        localparam int PROBABILITY_FRAC = 12;

        // LUT
        localparam int LUT_INPUT_W = 9;
        localparam int LUT_INPUT_FRAC = 5;

        localparam int LUT_PRODUCT_W = SUM_W + BETA_W;
        localparam int LUT_PRODUCT_FRAC = SUM_FRAC + BETA_FRAC;

        localparam int LUT_SHIFT = LUT_PRODUCT_FRAC - LUT_INPUT_FRAC;
        localparam int LUT_ROUND = 1 << (LUT_SHIFT - 1);
        
        localparam int LUT_SCALED_W = LUT_PRODUCT_W - LUT_SHIFT;
        localparam int LUT_SCALED_FRAC = LUT_INPUT_FRAC;

        localparam int LUT_CLAMP_HIGH = (1 << (LUT_INPUT_W - 1)) - 1;
        localparam int LUT_CLAMP_LOW = -(1 << (LUT_INPUT_W - 1));

        localparam int LUT_BIAS = LUT_INPUT_W - 1;

        localparam int LUT_ADDR_W = LUT_INPUT_W;

        localparam int LUT_DEPTH = 1 << LUT_INPUT_W;

        // FEEDER
        localparam int PBITS_PER_PLU = 6; 
        localparam int PBITS_PER_PLU_MAX = 16; 
        localparam int TERMS_PER_PBIT_MAX = 32;
        localparam int TERM_TOTAL_MAX = PBITS_PER_PLU_MAX*TERMS_PER_PBIT_MAX;

        localparam int INDEX_W = $clog2(PBITS_PER_PLU_MAX);

        localparam int PBIT_INDEX_W = $clog2(PBIT_NUM_MAX);
        localparam int PBIT_PROFILE_ADDRESS_W = $clog2(TERM_TOTAL_MAX);
        localparam int PBIT_TERM_COUNT_W = $clog2(TERMS_PER_PBIT_MAX + 1);
        localparam int INDEX_STRING_W = 1 + PBIT_INDEX_W + PBIT_PROFILE_ADDRESS_W + PBIT_TERM_COUNT_W;

        localparam int TERM_STRING_W = 2 + TERM_WEIGHT_W + 2*PBIT_INDEX_W;

        // UPDATER
        localparam int PLU_COUNT = 10;

        // CONTROLLER
        localparam int COLOR_COUNT_W = $clog2(PBITS_PER_PLU + 1);

        localparam int ROUND_COUNT = 32768;
        localparam int ROUND_COUNT_W = $clog2(ROUND_COUNT + 1);

        localparam int BETA_HOT = 615;
        localparam int BETA_DURATION = 4;
        localparam int BETA_SIGNAL = $clog2(BETA_DURATION);

    endpackage
