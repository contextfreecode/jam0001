const Person = struct {
    name: str,
    age: int,
};
const std = @import("std");
pub fn main() void {
    std.debug.print("Hi!\n", .{});
}
