interface I {
    function a() external;
}

contract Uninitialized{

    function func() external returns(uint){
        uint uint_not_init;
        uint uint_init = 1;
        return uint_not_init + uint_init;
    }

    function func_try_catch(I i) external returns(uint) {
        try i.a() {
            return 1;
        } catch (bytes memory data) {
            data;
        }
    }

}
