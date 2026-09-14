// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AccessControlVulnerable {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    // VULNERABILITY: Missing access control modifier (e.g., onlyOwner)
    // Anyone can call this and take over the contract
    function changeOwner(address newOwner) public {
        owner = newOwner;
    }

    // VULNERABILITY: Unprotected selfdestruct
    // Anyone can destroy the contract and steal the funds
    function destroy() public {
        selfdestruct(payable(owner));
    }
}
