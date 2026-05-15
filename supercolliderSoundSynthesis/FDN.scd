(
SynthDef(\fdnReverb, {
    |out=0, mix=0.3,
	/*feedback = 0.6
	feedback = 0.7
	feedback = 0.8*/
	feedback = 0.9|

    var input, local, delays, delayTimes, matrix, processed;
    var left, right, wet;

    // Input
	// input = SoundIn.ar(0);
    // input = Impulse.ar(1); // test signal
	input = EnvGen.ar(Env.perc(0.001, 0.01), doneAction: 0);

    // Delay times
	// delayTimes = [0.0297, 0.0371, 0.0411, 0.0437];

	// uniform delay---
	// delayTimes = [0.03, 0.03, 0.03, 0.03];

	// irregular delay---
	//delayTimes = [0.03, 0.035, 0.04, 0.045];

	// optimised delay---
	// delayTimes = [0.0297, 0.0371, 0.0411, 0.0437];

	// quasi-uniform delay--
	// delayTimes = [0.029, 0.0345, 0.0405, 0.047];

	// golden ratio delay--
	delayTimes = [0.0185,0.0299,0.0484,0.0783];


    // Feedback input
    local = LocalIn.ar(4);

    // Delay lines with damping
    delays = Array.fill(4, { |i|
        var d;
        d = DelayC.ar(local[i] + input, 0.1, delayTimes[i]);
        LPF.ar(d, 5000);
    });

    // Hadamard-like matrix
    matrix = [
        [ 1,  1,  1,  1],
        [ 1, -1,  1, -1],
        [ 1,  1, -1, -1],
        [ 1, -1, -1,  1]
    ] * 0.5;

    // Apply matrix
    processed = Array.fill(4, { |i|
        var sum = 0;
        4.do { |j|
            sum = sum + (matrix[i][j] * delays[j]);
        };
        sum * feedback;
    });

    // Feedback loop
    LocalOut.ar(processed);

    // Stereo output
    left  = processed[0] + processed[1];
    right = processed[2] + processed[3];

    wet = [left, right] * 0.5;

    // Output
    Out.ar(out, (input ! 2) * (1 - mix) + wet * mix);

}).add;
)
x = Synth(\fdnReverb);

// record
s.record;
s.stopRecording;



// 6x6 fdn

(
SynthDef(\fdnReverb6x6, {
    |out=0, mix=0.3, feedback=0.6|

    var input;
    var local;
    var delays;
    var delayTimes;
    var matrix;
    var processed;

    var left, right, wet;

    // =========================================
    // INPUT SIGNAL
    // =========================================

    // Softer excitation
    input = PinkNoise.ar(
        EnvGen.ar(
            Env.perc(0.001, 0.02),
            doneAction: 0
        ) * 0.08
    );

    // =========================================
    // DELAY TIMES
    // Better distributed / less resonant
    // =========================================

    delayTimes = [
        0.019,
        0.027,
        0.031,
        0.041,
        0.059,
        0.073
    ];

    // =========================================
    // LOCAL FEEDBACK
    // =========================================

    local = LocalIn.ar(6);

    // =========================================
    // DELAY NETWORK
    // =========================================

    delays = Array.fill(6, { |i|

        var d;

        d = DelayC.ar(
            local[i] + input,
            0.1,
            delayTimes[i]
        );

        // stronger HF damping
        d = LPF.ar(d, 2500);

        // extra attenuation for stability
        d = d * 0.95;

        d;
    });

    // =========================================
    // ORTHOGONAL-LIKE MATRIX
    // More stable normalization
    // =========================================

    matrix = [
        [ 1,  1,  1,  1,  1,  1],
        [ 1, -1,  1, -1,  1, -1],
        [ 1,  1, -1, -1,  1,  1],
        [ 1, -1, -1,  1, -1,  1],
        [ 1,  1,  1, -1, -1, -1],
        [ 1, -1,  1,  1, -1, -1]
    ] * 0.35;

    // =========================================
    // MATRIX MIXING
    // =========================================

    processed = Array.fill(6, { |i|

        var sum = 0;

        6.do { |j|

            sum = sum + (
                matrix[i][j] * delays[j]
            );

        };

        sum * feedback;
    });

    // =========================================
    // FEEDBACK LOOP
    // =========================================

    LocalOut.ar(processed);

    // =========================================
    // STEREO OUTPUT
    // =========================================

    left = (
        processed[0] +
        processed[1] +
        processed[2]
    ) * 0.33;

    right = (
        processed[3] +
        processed[4] +
        processed[5]
    ) * 0.33;

    wet = [left, right];

    // =========================================
    // OUTPUT MIX
    // =========================================

    Out.ar(
        out,
        ((input ! 2) * (1 - mix))
        +
        (wet * mix)
    );

}).add;
)


// =============================================
// RUN
// =============================================

x = Synth(\fdnReverb6x6);


// =============================================
// RECORD
// =============================================

// start recording
s.record;

// stop recording
s.stopRecording;