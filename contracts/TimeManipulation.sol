// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Roulette {
    uint256 public pastBlockTime;

    constructor() payable {}

    // VULNERABILITY: Using block.timestamp for randomness
    // Miners can manipulate the timestamp to win the lottery
    function spin() public payable {
        require(msg.value == 1 ether, "Must send 1 ether");
        require(block.timestamp != pastBlockTime, "Only 1 transaction per block");
        
        pastBlockTime = block.timestamp;
        
        if (block.timestamp % 15 == 0) {
            (bool sent, ) = msg.sender.call{value: address(this).balance}("");
            require(sent, "Failed to send Ether");
        }
    }
}
