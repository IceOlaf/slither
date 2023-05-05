interface ITestContract {
    event NoParams();
    event Anonymous();
    event OneParam(address);
    event OneParamIndexed(address);
    error ErrorWithEnum(uint8);
    error ErrorSimple();
    error ErrorWithArgs(uint256, uint256);
    error ErrorWithStruct(uint256);
    enum SomeEnum { ONE, TWO, THREE }
    struct St {
        uint256 v;
    }
    function stateA() external returns (uint256);
    function owner() external returns (address);
    function structs(address,uint256) external returns (uint256);
    function err0() external;
    function err1() external;
    function err2(uint256,uint256) external;
    function newSt(uint256) external returns (uint256);
    function getSt(uint256) external view returns (uint256);
    function removeSt(uint256) external;
}

