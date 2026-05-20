open Printf
open List

type point = { x : float; y : float }
type color = Red | Green | Blue

let distance p1 p2 =
    let dx = p1.x -. p2.x in
    let dy = p1.y -. p2.y in
    sqrt (dx *. dx +. dy *. dy)

let find_nearest points target =
    fold_left (fun acc p ->
        if distance p target < distance acc target then p else acc
    ) (hd points) (tl points)

let map_points f pts =
    map f pts

let color_to_string = function
    | Red   -> "red"
    | Green -> "green"
    | Blue  -> "blue"

let () =
    let p1 = { x = 0.0; y = 0.0 } in
    let p2 = { x = 3.0; y = 4.0 } in
    printf "Distance: %f\n" (distance p1 p2)
