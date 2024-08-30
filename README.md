# UGridAuction
Microgrid Multi Agent Auction Implementation using RIAPS. The algoritm is derrived from `A. L. Dimeas and N. D. Hatziargyriou, “Operation of a multiagent system for microgrid control,” IEEE Transactions on Power systems, vol. 20, no. 3, pp. 1447–1455, 2005`.

## Overview
The microgrid auction algorithm is for energy exchange between producers and consumers. The auction process can essentially be treated as an optimal resource allocation problem. A multiagent system based implementation of the algorithm is presented here. It is based on the symmetric matching problem which aims to find the optimal assignment of local buyers to sellers to maximize a given benefit 
$$max \sum_{i=1}^{n} a_{bs}$$
where $a_{bs}$ is the benefit for matching buyer b with seller s and n is the number of buyers/ sellers.

## Phases
The algorithm proceeds in two phases:
- **Bidding**: In the first phase, each buyer determines the seller that it is interested in and calculates a bid for it. This is done by determining the seller with the maximum net value.
  $$s_b \in max \left( a_{bs} - p_s \right)$$,
where $s_b$ is the seller that buyer b is interested in, $a_bs$ is the benefit of seller s for buyer b and $p_s$ is the price assigned to seller s. The price is an algorithmic variable, different from the market price. This price is incremented in each round according to the bid. The bid amount is calculated using the difference between the highest net seller value $u_b$ and the second highest net seller value $v_b$.
$$\gamma_b = u_b - v_b + \epsilon$$
$\epsilon$ is a small value that is added to the bid to ensure that the algorithm progresses.

- **Assignent**: In this phase the sellers determine the highest bidders from the bids that they receive.
  $$b_s = max{\gamma_b}$$,
where $b_s$ is the buyer that bid the maximum for seller s.
Following that, the sellers increment their prices by the highest bidding amount and get assigned to that corresponding buyer. If the seller was previously assigned to a different buyer, then that buyer is freed. The algorithm proceeds accordingly until all buyers have been matched to sellers.

It is proven that the algorithm terminates in a finite number of iterations if $\epsilon < \frac{1}{n}$.

## Implementation

The example impleents a distibuted vesion of te above application nconsisiting of a buyer, a seller and a market component. It adds fault tolerant properties to the algorithm as highlighted by the fault scenarios given below.

| Fault | Fault Location | Detection | Response Strategy |
|-------|----------------|-----------|--------------------|
| Market node crashes| Market node crashes| Heartbeat (Intrinsic)| Active Replication - Have a group of Market nodes out of which one acts as the active leader. Followers detect if the leader is offline and in that case elect a new leader and switch over to it. The leader sends its current state to all followers periodically.|
| Buyer crashes before bidding.| Buyer node| Heartbeat (Intrinsic)| Seller identifies which buyer is off. If it has received bids from all other buyers, then it proceeds with assignment.|
| Buyer node crashes after assignment| Buyer node| Heartbeat (Intrinsic) |Seller identifies which buyer is off. If it was assigned to that buyer then it frees itself for the next round.|
|Seller node crashes before sending price information| Seller node| Heartbeat (Intrinsic)| Buyer identifies which seller is off. If it was assigned to that seller then it frees itself. If the buyer has received prices from all other sellers then it starts the bidding phase.|
| Seller node crashes after sending price information| Seller node| Heartbeat (Intrinsic)| Buyer identifies which seller is off ad frees itself if it was assigned to it. It ignores the price received from that seller and proceeds with the others. |
