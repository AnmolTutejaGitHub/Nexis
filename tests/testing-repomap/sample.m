#import <Foundation/Foundation.h>

@protocol Fetchable <NSObject>
- (NSArray *)fetchItems;
- (BOOL)saveItem:(NSDictionary *)item;
@end

@interface DataManager : NSObject <Fetchable>
@property (nonatomic, strong) NSDictionary *config;
- (instancetype)initWithConfig:(NSDictionary *)config;
- (NSArray *)fetchItems;
- (BOOL)saveItem:(NSDictionary *)item;
- (void)clearCache;
@end

@implementation DataManager

- (instancetype)initWithConfig:(NSDictionary *)config {
    self = [super init];
    if (self) {
        _config = config;
    }
    return self;
}

- (NSArray *)fetchItems {
    return @[];
}

- (BOOL)saveItem:(NSDictionary *)item {
    return item != nil;
}

- (void)clearCache {
    NSLog(@"Cache cleared");
}

@end
