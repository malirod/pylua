function inc(initial_value, count)
    result = initial_value
    for i=1, count do
        result = result + 1
    end
    return result
end

print("Testing: ")
test = inc(5, 10)
print(test)
