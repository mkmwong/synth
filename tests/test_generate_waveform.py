from synth.waveform import *
from typing import Tuple
import pytest


# test wave generation value error
def test_generate_waveform_invalid_input():
    with pytest.raises(ValueError):
        generate_waveform(type="sin")


# testing wave generation return type
@pytest.mark.parametrize("test_type", ["sine", "sawtooth", "triangle", "square"])
def test_return_type_from_generate_waveform(test_type):
    res = generate_waveform(type=test_type)
    # checking return type
    assert isinstance(
        res, tuple
    ), f"{test_type}: Tuple should be returned from calling generate_waveform"
    assert isinstance(
        res[0], np.ndarray
    ), f"{test_type}: Waveform returned from generate_waveform should be numpy array"
    assert isinstance(res[1], int), f"{test_type}: Sampling rate returned should be int"


@pytest.mark.parametrize("test_type", ["sine", "sawtooth", "triangle", "square"])
def test_waveform_length(test_type):
    duration = 3.0
    frequency = 220.0
    sampling_rate = 22000
    res = generate_waveform(duration, frequency, sampling_rate, type=test_type)
    assert len(res[0]) == int(duration * sampling_rate)


@pytest.mark.parametrize("test_type", ["sine", "sawtooth", "triangle", "square"])
def test_waveform_value_range(test_type):
    duration = 3.0
    frequency = 220.0
    sampling_rate = 22000
    res = generate_waveform(duration, frequency, sampling_rate, type=test_type)
    min_value = -1
    max_value = 1
    is_in_range = np.all((res[0] >= min_value) & (res[0] <= max_value))
    assert is_in_range == True


@pytest.mark.parametrize("test_type", ["sine", "sawtooth", "triangle", "square"])
@pytest.mark.parametrize("duration", [1.0, 10.0, 100.0])
def test_waveform_duration_change(test_type, duration):
    frequency = 220.0
    sampling_rate = 22000
    res = generate_waveform(duration, frequency, sampling_rate, type=test_type)

    assert len(res[0]) == int(duration * sampling_rate)


@pytest.mark.parametrize("test_type", ["sine", "sawtooth", "triangle", "square"])
@pytest.mark.parametrize("frequency", [1.0, 10.0, 100.0])
def test_waveform_frequency_change(test_type, frequency):
    duration = 3.0
    sampling_rate = 22000
    res = generate_waveform(duration, frequency, sampling_rate, type=test_type)
    assert len(res[0]) == int(duration * sampling_rate)


# 3. frequency working correctly : # of zero crossings ~ 2*freq (for sine wave )  / periodicity
