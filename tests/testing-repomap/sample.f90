module math_utils
    implicit none

contains

    function factorial(n) result(res)
        integer, intent(in) :: n
        integer :: res, i
        res = 1
        do i = 2, n
            res = res * i
        end do
    end function factorial

    function gcd(a, b) result(res)
        integer, intent(in) :: a, b
        integer :: res, x, y
        x = a; y = b
        do while (y /= 0)
            res = mod(x, y)
            x = y; y = res
        end do
        res = x
    end function gcd

    subroutine normalize(arr, n)
        integer, intent(in) :: n
        real, intent(inout) :: arr(n)
        real :: max_val
        max_val = maxval(arr)
        if (max_val /= 0.0) arr = arr / max_val
    end subroutine normalize

    subroutine print_array(arr, n)
        integer, intent(in) :: n
        integer, intent(in) :: arr(n)
        integer :: i
        do i = 1, n
            print *, arr(i)
        end do
    end subroutine print_array

end module math_utils
