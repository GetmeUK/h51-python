import h51


client = h51.Client(
    'gY4uNgniLM6gps60dyYKDKklBVlb7zh8xUqI9ZBp2aLd4KOsEeQrrfNViPiQ_0Hbcu_frZ8BbwMOaWPfnpTaxGAaD93_BAr6nBA6uw6Id0Cgm4OCcG5MDi93aXMjsBkC0oYd9_sED_WaJLrg3S83A0RXd2sDqQobmKwZIGu5AHM',
    api_base_url='http://api.h51.local'
)

asset = h51.resources.Asset.one(client, '3owuun')

# r = h51.resources.Variation.create_many(
#     client,
#     ['3owuun', 'xvr8dj'],
#     {
#         '3owuun': {
#             'x1': [
#                 h51.transforms.images.AutoOrient(),
#                 h51.transforms.images.FocalPointCrop(aspect_ratio=0.5),
#                 h51.transforms.images.Fit(640, 640),
#                 h51.transforms.images.Output('WebP')
#             ]
#         },
#         'xvr8dj': {
#             'x1': [
#                 h51.transforms.images.AutoOrient(),
#                 h51.transforms.images.FocalPointCrop(aspect_ratio=0.5),
#                 h51.transforms.images.Fit(640, 640),
#                 h51.transforms.images.Output('JPEG')
#             ]
#         }
#     },
#     local=True
# )

r = h51.resources.Asset.analyze_many(
    client,
    ['3owuun', 'ayj6wc'],
    {
        '3owuun': [
            h51.analyzers.images.DominantColors(),
            h51.analyzers.images.FocalPoint()
        ],
        'ayj6wc': [
            h51.analyzers.images.Animation()
        ]
    },
    local=True
)

print(r)
