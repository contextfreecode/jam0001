const Person = struct {
    /// Could be full name or just preferred name.
    name: str,
    /// Age in years from birth or manufacture date rounded down.
    age: int,
};
const Car = struct {
    driver: Person,
    model: str,
    /// Age in years from birth or manufacture date rounded down.
    age: int,
};
const Detail = struct {
    /// Age in years from birth or manufacture date rounded down.
    age: float,
};
const std = @import("std");
pub fn main() void {
    std.debug.print("Hi!\n", .{});
}
