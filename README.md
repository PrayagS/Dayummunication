<h1 align="center">
  Dayummunication
</h1>

<h3 align="center">
	Dashboard for learning digital communication techniques
</h3>

<p align="center">
	<strong>
		<a href="https://dayummunication.herokuapp.com/">Demo</a>
	</strong>
</p>

<p align="center">
	<img src="https://github.com/PrayagS/Dayummunication/blob/master/images/dashboard.png?raw=true">
</p>

<p align="center">
  <strong>
    <a href="#introduction">Introduction</a> •
    <a href="#specifications">Specifications</a> •
    <a href="#block-diagrams">Block Diagrams</a> •
    <a href="#flowchart">Flowchart</a> •
     <a href="#results">Results</a>
  </strong>
</p>

---

## Introduction
A digital communication system utilizes a mode of communication where information is encoded digitally as discrete signals and electronically transferred to the recipients. Digital communication systems are omnipresent and play a vital role in today’s world. With the right technology, data can be transmitted over a large distance.

A typical digital communication system consists of a transmitter, a channel and a receiver. The digital data (0s and 1s) is typically “modulated”, i.e., converted into signals which are optimised for transmission. The modulated signal is transmitted over a channel, where noise gets added. Signal loses power i.e. signal attenuation occurs and this loss is generally different for different frequencies. Hence, the channel also acts as a filter. Finally, at the receiving end, there is a demodulator which converts the waveforms back to digital information.

Since the received signal is not exactly the same as the transmitted signal, there will sometimes be errors in the received information. These errors can be quantified numerically if information about the channel is known.

In this project, we simulate a complete digital communication system whose details will be shared in the further sections.

## Specifications

### Parameters

The system functions on the following received parameters:

- Bit Energy
- Bit Time
- Carrier Frequency
- Sampling Frequency
- Noise Power Spectral Density
- Input Signal
- Whether or not to apply coding scheme (discussed later)

### Transmitter

Information is received from the user and converted to bits. These bits are encoded for error correction (more on that later). Thereafter, the bits are modulated. We simulate the following modulation techniques:

- Binary Phase Shift Keying (BPSK)

- Quadrature Phase Shift Keying (QPSK)

- Binary Frequency Shift Keying (BFSK)

- Quadrature Frequency Shift Keying (QFSK)

	We have also attempted to generalize PSK by writing code for M-Ary Phase Shift Keying (MPSK) which can perform modulation/demodulation for a given value of 'M'. But since the error performance was highly unsatisfactory, we are not using it. (Pull requests welcome!) 
	Data given by the user is modulated using the technique of his choice and converted to waveforms. 

### Channel
The channel is simulated by adding [Additive White Gaussian Noise](https://en.wikipedia.org/wiki/Additive_white_Gaussian_noise) (AWGN) of the desired Power Spectral Density. The noise distorts the waveforms. Finally, the signal is demodulated and the bit error rate is calculated. The same is compared with the theoretically expected value. 
	The noteworthy characteristics of Additive White Gaussian Noise which need to be considered are:

- The samples follow a normal distribution in the time domain, i.e., they follow a Gaussian distribution with mean 0 and variance 1.

- The power across the frequency band is uniform. 

- The samples are assumed to be independent and identically distributed (iid).
	Practically, it would be impossible to generate such a signal. But we can approximately obtain it. Following is the distribution of power spectral density across frequencies for 1000 samples we generate:
	
	<h5 align="center">
	  <img src="https://github.com/PrayagS/Dayummunication/blob/master/images/plots/psd.png?raw=true">
	</h5>
	
	We infer that the values are comparable when a large number of bits are transmitted. The same will be discussed in the results section. 

### Receiver
The receiver demodulates the signal based on the chosen method of demodulation. Thereafter, the signal is decoded using the extended Golay decoding scheme. 
	For the sake of demonstration, we perform bit error analysis where the theoretical and practical values are compared. The same is discussed in the results section.

### Error correction coding
We use extended binary Golay code G24 to reduce the Bit Error Rate (BER). The extended Golay code encodes 12 bits of data in 24 words such that any 3-bit errors can be corrected or 7-bit errors can be detected. The standard coding notation for this code in terms of [n,k,d] is [24,12,8]. We use an existing Python implementation found in a GitHub repository and modify it for our purposes. (See credits)
The bit error probability formula changes in this case and that is,
$$
P_b = \frac{1}{n}\Sigma_{j=t+1}^{n}j \cdot {{n}\choose{j}}\cdot p_c^j \cdot (1-p_c)^{n-j}
$$
Where pc is the bit error probability without encoding, t is the number of correctable errors (3) and n is the encoded size (24).

## Technology Stack

- Python as the primary language
- Scipy and NumPy for scientific computation, inbuilt functions and array operations
- Matplotlib for testing on backend and error analysis
- Dash (Plotly) for the web application with dynamically updating results.

## Block Diagrams

### Communication System
#### Transmitter
<h5 align="center">
  <img src="https://github.com/PrayagS/Dayummunication/blob/master/images/block_diagrams/transmitter.png?raw=true">
</h5>

#### Receiver
<h5 align="center">
  <img src="https://github.com/PrayagS/Dayummunication/blob/master/images/block_diagrams/receiver.png?raw=true">
</h5>

### BFSK
#### Modulator
<h5 align="center">
  <img src="https://github.com/PrayagS/Dayummunication/blob/master/images/block_diagrams/BFSK_M.png?raw=true">
</h5>

#### Demodulator
<h5 align="center">
  <img src="https://github.com/PrayagS/Dayummunication/blob/master/images/block_diagrams/BFSK_D.png?raw=true">
</h5>

### QFSK
#### Modulator
<h5 align="center">
  <img src="https://github.com/PrayagS/Dayummunication/blob/master/images/block_diagrams/QFSK_M.png?raw=true">
</h5>

#### Demodulator
<h5 align="center">
  <img src="https://github.com/PrayagS/Dayummunication/blob/master/images/block_diagrams/QFSK_D.png?raw=true">
</h5>

### BPSK
#### Modulator
<h5 align="center">
  <img src="https://github.com/PrayagS/Dayummunication/blob/master/images/block_diagrams/BPSK_M.png?raw=true">
</h5>

#### Demodulator
<h5 align="center">
  <img src="https://github.com/PrayagS/Dayummunication/blob/master/images/block_diagrams/BPSK_D.png?raw=true">
</h5>

### QPSK
#### Modulator
<h5 align="center">
  <img src="https://github.com/PrayagS/Dayummunication/blob/master/images/block_diagrams/QPSK_M.png?raw=true">
</h5>

#### Demodulator
<h5 align="center">
  <img src="https://github.com/PrayagS/Dayummunication/blob/master/images/block_diagrams/QPSK_D.png?raw=true">
</h5>

## Flowchart
<h3 align="center">
  <img src="https://github.com/PrayagS/Dayummunication/blob/master/images/block_diagrams/flowchart.png?raw=true">
</h3>

## Results
### BER vs SNR for different modulation techniques. 
These results were generated by performing Monte Carlo simulations to generate an array of random samples and transmitting it over our AWGN channel. The BER was calculated by comparing the received and sent array of samples.

#### BPSK
| ![](https://github.com/PrayagS/Dayummunication/blob/master/images/plots/BPSK_The2.png?raw=true) | ![](https://github.com/PrayagS/Dayummunication/blob/master/images/plots/BPSK_BER.png?raw=true) |
| :---: | :---: |
| Theoretical | Practical |

#### QPSK
| ![](https://github.com/PrayagS/Dayummunication/blob/master/images/plots/QPSK_The2.png?raw=true) | ![](https://github.com/PrayagS/Dayummunication/blob/master/images/plots/QPSK_BER.png?raw=true) |
| :---: | :---: |
| Theoretical | Practical |

#### BFSK
| ![](https://github.com/PrayagS/Dayummunication/blob/master/images/plots/BFSK_The2.png?raw=true) | ![](https://github.com/PrayagS/Dayummunication/blob/master/images/plots/BFSK_BER.png?raw=true) |
| :---: | :---: |
| Theoretical | Practical |

#### QFSK
| ![](https://github.com/PrayagS/Dayummunication/blob/master/images/plots/QFSK_The2.png?raw=true) | ![](https://github.com/PrayagS/Dayummunication/blob/master/images/plots/QFSK_BER.png?raw=true) |
| :---: | :---: |
| Theoretical | Practical |

### Image transmission ([image used](http://www.ece.rice.edu/~wakin/images/))
This was done by converting the image to a matrix of RGB values. Each value in that matrix was converted to binary and the obtained matrix was transmitted over our AWGN channel. At the receiving end, the matrix is again converted to the matrix of RGB values from which the image is generated.

#### BPSK
| ![](https://github.com/PrayagS/Dayummunication/blob/master/images/test_images/lena256color.png?raw=true) | ![](https://github.com/PrayagS/Dayummunication/blob/master/images/test_images/encoded_lena256color_decoded_BPSK.png?raw=true) |
| :---: | :---: |
| Sent | Received |

#### QPSK
| ![](https://github.com/PrayagS/Dayummunication/blob/master/images/test_images/lena256color.png?raw=true) | ![](https://github.com/PrayagS/Dayummunication/blob/master/images/test_images/encoded_lena256color_decoded_QPSK.png?raw=true) |
| :---: | :---: |
| Sent | Received |

#### BFSK
| ![](https://github.com/PrayagS/Dayummunication/blob/master/images/test_images/lena256color.png?raw=true) | ![](https://github.com/PrayagS/Dayummunication/blob/master/images/test_images/encoded_lena256color_decoded_BFSK.png?raw=true) |
| :---: | :---: |
| Sent | Received |

#### QFSK
| ![](https://github.com/PrayagS/Dayummunication/blob/master/images/test_images/lena256color.png?raw=true) | ![](https://github.com/PrayagS/Dayummunication/blob/master/images/test_images/encoded_lena256color_decoded_QFSK.png?raw=true) |
| :---: | :---: |
| Sent | Received |




## Team

[![Prayag Savsani](https://avatars2.githubusercontent.com/u/44412790?s=400&u=b8e40515644dc045ad5773dd1b6ded812d84d6b9&v=4)](https://github.com/PrayagS)  | [![Yashraj Kakkad](https://avatars0.githubusercontent.com/u/18521104?s=400&u=0b8ff7367cb07eba2014fb5be62cb0d89c38567a&v=4)](https://github.com/yashrajkakkad) | [![Kaushal Patil](https://avatars0.githubusercontent.com/u/50149591?s=400&u=e459fcc83d75c0c545ed7da2348feffe39206a32&v=4)](https://github.com/Kaushal1011) | [![Dhruvil Dave](https://avatars1.githubusercontent.com/u/43331416?s=400&u=f31cb03c456f103f87210810d46ed3832fb100e0&v=4)](https://github.com/dhruvildave)
---|---|---|---|
[Prayag Savsani](https://github.com/PrayagS) | [Yashraj Kakkad](https://github.com/yashrajkakkad) | [Kaushal Patil](https://github.com/Kaushal1011) | [Dhruvil Dave](https://github.com/dhruvildave)

## [License](https://github.com/PrayagS/Dayummunication/blob/master/LICENSE)

BSD 3-Clause "New" or "Revised" License
