function (initial_value, count)
    local result = initial_value
    for i=1, count do
        result = result + 1
    end
    return result
end
