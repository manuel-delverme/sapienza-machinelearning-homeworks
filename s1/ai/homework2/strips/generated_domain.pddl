(define (domain paul-world)
    (:predicates
        (can-move ?from ?to)
        (is-in ?object ?square)
        ;;(been-at ?robot ?square)
        (carry ?robot ?object)
        (at ?robot ?square)
        (square ?square)
        (wall ?wall)
        (robot ?robot)
        (empty ?robot)
    )

    (:action move
        :parameters
            (?robot
             ?from-square
             ?to-square)

        :precondition
            (and
                (robot ?robot)
                (square ?from-square)
                (square ?to-square)

                (at ?robot ?from-square)
                (can-move ?from-square ?to-square)
            )

        :effect
            (and
                (at ?robot ?to-square)
                (not
                  (at ?robot ?from-square)
                )
            )
    )
)
    